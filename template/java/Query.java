import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.lar.book.BookEntity;
import lombok.Data;
import lombok.EqualsAndHashCode;

import javax.validation.constraints.NotNull;

{% set table = config.table|capitalize %}
@Data
@EqualsAndHashCode(callSuper = false)
public class {{table}}Query extends Page<{{table}}Entity> {
    {% for item in config.list -%}
    private String {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endfor %}
}