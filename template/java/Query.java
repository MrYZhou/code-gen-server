{% set table = config.table|capitalize -%}
{% set modelName = config.modelName -%}
package jnpf.base.model.{{config.table|lower}};
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import java.util.Date;
import lombok.Data;
import lombok.EqualsAndHashCode;
import jnpf.base.entity.{{table}}Entity;
import javax.validation.constraints.NotNull;



@Data
@EqualsAndHashCode(callSuper = false)
public class {{modelName}}Query extends Page<{{modelName}}Entity> {
    {% for item in config.list -%}
    {% set fieldName = item.columnName|replace(config.fieldPrefix, "") -%}
    {% if fieldName in  config.searchList -%}
    /**{{ item.columnComment  }}*/
    {% if item.dataType == 'datetime' -%}
    private Date {{fieldName}};
    {% elif item.dataType == 'decimal' -%}
    private BigDecimal {{fieldName}};
    {% else -%}
    private String {{fieldName}};
    {% endif -%}
    {% endif -%}
    {% endfor %}
}