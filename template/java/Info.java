

{% set modelName = config.modelName -%}
package jnpf.base.model.{{config.table|lower}};
import lombok.Data;

@Data
public class {{modelName}}Info {
    {% for item in config.list -%}
    {% if item.dataType == 'datetime' -%}
    private Date {{item.columnName|replace(config.fieldPrefix, "")}};
    {% elif item.dataType == 'decimal' -%}
    private BigDecimal {{item.columnName|replace(config.fieldPrefix, "")}};
    {% else -%}
    private String {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endif -%}
    {% endfor %}
}
