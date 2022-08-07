@Override
public List<TenantFlowVO> selectAllFlow(TenantFlowPage pagination) {
    TenantEntity tenant = this.getInfo(pagination.getTenantId());
    pagination.setDbName(tenant.getDbName());
    pagination.setDbEnCode(tenant.getEnCode());
    //        DataSourceContextHolder.setDatasource(tenant.getEnCode(), tenant.getDbName());
    
    Map<String,Object> result = tenantFlowApi.tenantFlowList(pagination);
    Long total = Long.parseLong(String.valueOf(result.get("total")));
    
    
    List<TenantFlowEntity> records = ( List<TenantFlowEntity>) result.get("list");
    if(records.size()==0){
        return pagination.setData(new ArrayList<>(), 0L);
    }
    
    
    List<TenantFlowVO> list = new ArrayList<>();
    if (records!=null && !records.isEmpty()) {
        list = JsonUtil.getJsonToList(records, TenantFlowVO.class);
        list = list.stream().map(t->{
            t.setTenantId(tenant.getId());
            t.setTenantName(tenant.getFullName());
            t.setTenantDbName(tenant.getDbName());
            return t;
        }).collect(Collectors.toList());
    }
    return pagination.setData(list, total);
    }