

import com.alibaba.fastjson.annotation.JSONField;
import com.baomidou.mybatisplus.annotation.*;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonProperty;


@Data
@TableName("{{config.table}}")
public class {{ config.modelName }}Entity {
    {% for item in config.list -%}
    {% if item.columnComment  -%}
    /**
    {{ item.columnComment  }}
     */
    {% endif -%}
    {% if loop.index0 == 0 -%}
    @TableId("{{item.columnName}}")
    {% endif -%}
    @TableField(name = "{{item.columnName}}")
    private {% if item.dataType == 'datatime' -%}
    Date
    {% else %}
    String
    {% endif -%}
    {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endfor %}
}
