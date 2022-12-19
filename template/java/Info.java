

import lombok.Data;

@Data
public class {{config.table|capitalize}}Info {
    {% for item in config.list -%}
    private String {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endfor %}
}
