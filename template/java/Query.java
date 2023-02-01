{% set table = config.table|capitalize -%}
{% set modelName = config.modelName -%}
package jnpf.base.model.{{config.table|lower}};
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import java.util.Date;
import lombok.Data;
import lombok.EqualsAndHashCode;
import jnpf.base.entity.{{modelName}}Entity;
import javax.validation.constraints.NotNull;
import java.util.List;


@Data
@EqualsAndHashCode(callSuper = false)
public class {{modelName}}Query extends Page<{{modelName}}Entity> {
    {% for item in config.list -%}
    {% set fieldName = item.columnName|replace(config.fieldPrefix, "") -%}
    
    /**{{ item.columnComment  }}*/
    {% if item.dataType == 'datetime' -%}
    private List<Date> {{fieldName}};
    {% elif item.dataType == 'decimal' -%}
    private BigDecimal {{fieldName}};
    {% else -%}
    private String {{fieldName}};
    {% endif -%}

    {% endfor %}

    
}