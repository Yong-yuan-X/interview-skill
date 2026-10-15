"""计算已由模型完成证据评估的评分；仅使用 Python 标准库。"""

import argparse
import json
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


RUBRIC_PATH = Path(__file__).resolve().parents[1] / "assets" / "rubrics.json"
ANSWER_STATUSES = {"answered", "explicitly_unknown", "skipped", "incorrect"}
EVIDENCE_STATUSES = {"sufficient", "not_assessed", "insufficient"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_fields(value, required, optional, path):
    require(isinstance(value, dict), f"{path}: 必须是对象")
    require(required <= value.keys(), f"{path}: 缺少字段 {sorted(required - value.keys())}")
    require(value.keys() <= required | optional,
            f"{path}: 未知字段 {sorted(value.keys() - required - optional, key=str)}")


def check_text(value, path):
    require(isinstance(value, str) and bool(value.strip()), f"{path}: 必须是非空字符串")


def number(value, path):
    # bool 在 Python 中属于 int，但不是合法权重。
    require(type(value) in (int, float, Decimal), f"{path}: 必须是有限数值，不能是布尔值或字符串")
    require(not isinstance(value, float) or math.isfinite(value), f"{path}: 必须是有限数值")
    result = Decimal(str(value))
    require(result.is_finite(), f"{path}: 必须是有限数值")
    return result


def validate_weights(weights, dimension_ids):
    check_fields(weights, set(dimension_ids), set(), "weights")
    result = {key: number(value, f"weights.{key}") for key, value in weights.items()}
    require(all(0 <= value <= 100 for value in result.values()), "weights: 每项必须在 0–100 之间")
    require(sum(result.values()) == 100, "weights: 总和必须为 100，不自动归一化非法配置")
    return result


def reject_constant(value):
    raise ValueError(f"JSON: 不允许非有限数值 {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON: 重复字段 {key}")
        result[key] = value
    return result


def parse_json(text):
    """拒绝重复键、NaN、Infinity；保留十进制输入以校验权重总和。"""
    return json.loads(text, parse_float=Decimal, parse_constant=reject_constant,
                      object_pairs_hook=unique_object)


def load_rubrics():
    return parse_json(RUBRIC_PATH.read_text(encoding="utf-8"))


def validate_answers(answers):
    require(isinstance(answers, list), "answers: 必须是数组")
    result = {}
    required = {"id", "question_id", "status", "text", "record_kind", "feedback_intervened"}
    for index, answer in enumerate(answers):
        path = f"answers[{index}]"
        check_fields(answer, required, set(), path)
        for field in ("id", "question_id", "text"):
            check_text(answer[field], f"{path}.{field}")
        require(answer["id"] not in result, f"{path}.id: 回答编号重复")
        require(isinstance(answer["status"], str) and answer["status"] in ANSWER_STATUSES,
                f"{path}.status: 非法回答状态")
        require(answer["record_kind"] in ("raw", "summary"), f"{path}.record_kind: 必须是 raw 或 summary")
        require(type(answer["feedback_intervened"]) is bool, f"{path}.feedback_intervened: 必须是布尔值")
        result[answer["id"]] = answer
    return result


def validate_ratings(ratings, dimension_ids, levels, answers):
    check_fields(ratings, set(dimension_ids), set(), "ratings")
    for dimension_id, rating in ratings.items():
        path = f"ratings.{dimension_id}"
        check_fields(rating, {"level", "evidence_status", "evidence"}, set(), path)
        level, status = rating["level"], rating["evidence_status"]
        require(isinstance(level, str) and level in (*levels, "N/A"), f"{path}.level: 非法等级")
        require(isinstance(status, str) and status in EVIDENCE_STATUSES,
                f"{path}.evidence_status: 非法证据状态")
        require((level != "N/A") == (status == "sufficient"),
                f"{path}: 仅 sufficient 可以评级，其他状态必须为 N/A")
        require(isinstance(rating["evidence"], list), f"{path}.evidence: 必须是数组")
        require(status != "sufficient" or bool(rating["evidence"]), f"{path}: 评级必须有回答证据")
        require(status != "not_assessed" or not rating["evidence"], f"{path}: 未考察不能附有回答证据")
        seen = set()
        for index, evidence in enumerate(rating["evidence"]):
            evidence_path = f"{path}.evidence[{index}]"
            check_fields(evidence, {"answer_id", "reason"}, set(), evidence_path)
            check_text(evidence["answer_id"], f"{evidence_path}.answer_id")
            check_text(evidence["reason"], f"{evidence_path}.reason")
            answer_id = evidence["answer_id"]
            require(answer_id in answers, f"{evidence_path}: 引用了不存在的回答 {answer_id}")
            require(answer_id not in seen, f"{evidence_path}: 同一维度重复引用同一回答")
            seen.add(answer_id)
            if status == "sufficient":
                require(answers[answer_id]["status"] != "skipped", f"{evidence_path}: 主动跳过不能作为能力评级证据")
                require(not answers[answer_id]["feedback_intervened"],
                        f"{evidence_path}: 指导后回答不能计入独立作答评分")


def rounded(value):
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calculate_score(data, rubrics):
    """纯函数：验证证据引用后加权；不读取文件，不判断自然语言能力。"""
    check_fields(data, {"interview_type", "critical_dimensions", "answers", "ratings"}, {"weights"}, "input")
    interview_type = data["interview_type"]
    require(isinstance(interview_type, str) and interview_type in rubrics["interview_types"],
            "interview_type: 必须是 technical、comprehensive 或 hr")
    dimensions = rubrics["interview_types"][interview_type]["dimensions"]
    dimension_ids = [dimension["id"] for dimension in dimensions]
    weights = validate_weights(data.get("weights", {d["id"]: d["weight"] for d in dimensions}), dimension_ids)
    critical = data["critical_dimensions"]
    require(isinstance(critical, list) and all(isinstance(key, str) for key in critical),
            "critical_dimensions: 必须是维度编号数组")
    require(len(set(critical)) == len(critical), "critical_dimensions: 不能重复")
    require(set(critical) <= set(dimension_ids), "critical_dimensions: 包含未知维度")
    answers = validate_answers(data["answers"])
    levels = rubrics["levels"]
    validate_ratings(data["ratings"], dimension_ids, levels, answers)

    coverage, weighted = Decimal(0), Decimal(0)
    rows = []
    for dimension in dimensions:
        key = dimension["id"]
        rating, weight = data["ratings"][key], weights[key]
        if rating["evidence_status"] == "sufficient":
            coverage += weight
            weighted += weight * number(levels[rating["level"]]["coefficient"], "coefficient")
        rows.append({"id": key, "name": dimension["name"], "weight": float(weight),
                     "level": rating["level"], "evidence_status": rating["evidence_status"],
                     "evidence": [dict(item) for item in rating["evidence"]]})

    missing = [key for key in critical if data["ratings"][key]["evidence_status"] != "sufficient"]
    reasons = []
    if not critical:
        reasons.append("未定义岗位关键能力，保留模拟招聘判断")
    if missing:
        reasons.append("岗位关键能力证据不足，保留模拟招聘判断")
    if coverage == 0:
        reasons.append("证据不足：没有具备充分证据且权重大于零的可评分维度")
    return {
        "interview_type": interview_type,
        "score": rounded(weighted / coverage * 100) if coverage else None,
        "coverage_percent": float(coverage),
        "dimensions": rows,
        "critical_dimensions": list(critical),
        "unassessed_critical_dimensions": missing,
        "judgment_status": "reserved" if reasons else "requires_model_judgment",
        "notes": reasons,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="从 JSON 计算评分；默认从标准输入读取，仅输出到标准输出。")
    parser.add_argument("input", nargs="?", default="-", help="UTF-8 JSON 文件，或 - 表示标准输入")
    args = parser.parse_args(argv)
    try:
        text = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8-sig")
        result = calculate_score(parse_json(text), load_rubrics())
    except (ValueError, OSError, UnicodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
