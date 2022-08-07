@Data
public class TenantFlowPage extends PaginationVO {

    private Date startTime;
    private Date endTime;
    private String keyword;
    private String dbName;
    private String dbEnCode;
    @NotNull(message = "租户信息缺失")
    private String tenantId;
    @ApiModelProperty(hidden = true)
    private String sort="desc";
    @ApiModelProperty(hidden = true)
    private String sidx="";


    public <T> List<T> setData(List<T> data, Long records) {
        this.setTotal(Math.toIntExact(records));
        return data;
    }

}