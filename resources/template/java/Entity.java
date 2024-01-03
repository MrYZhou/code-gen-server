
{% set modelName = config.modelName -%}
package jnpf.base.entity;
import com.alibaba.fastjson.annotation.JSONField;
import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonProperty;


@Data
@TableName("{{config.tableName}}")
public class {{ modelName }}Entity {
    {% for item in config.list -%}
    {% if item.columnComment  -%}
    /**
    {{ item.columnComment  }}
     */
    {%- endif -%}
    {% if loop.index0 == 0 -%}
    @TableId("{{item.columnBase}}")
    private String  {{item.columnName|replace(config.fieldPrefix, "")}};
    {% else %}
    @TableField("{{item.columnBase}}")
    {% if item.dataType == 'datetime' -%}
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", locale = "zh")
    private Date {{item.columnName|replace(config.fieldPrefix, "")}};
    {% elif item.dataType == 'decimal' -%}
    private BigDecimal {{item.columnName|replace(config.fieldPrefix, "")}};
    {% else -%}
    private String {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endif -%}
    
    {% endif -%}
    
    {% endfor %}
}
