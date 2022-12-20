

import lombok.Data;

@Data
public class {{config.table|capitalize}}Info {
    {% for item in config.list -%}
    private {% if item.dataType == 'datatime' -%}
    Date
    {% else %}
    String
    {% endif -%}
    String {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endfor %}
}
