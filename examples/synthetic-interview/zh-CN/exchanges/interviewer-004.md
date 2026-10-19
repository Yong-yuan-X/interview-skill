换到列表查询。工单表已有索引 `(tenant_id, status, created_at DESC, id DESC)`。如果请求只按租户筛选、不传状态，仍按 `created_at DESC, id DESC` 排序分页，你会怎样分析这条索引对这次查询的帮助和限制？
