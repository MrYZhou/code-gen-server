package com.{{config.table}};

import lombok.Data;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;


@Table(name = "{{config.table}}")
@Entity
@Data
public class {{ config.modelName }}Entity {
    {% for item in config.list -%}
    {% if item.columnComment  -%}
    /**
    {{ item.columnComment  }}
     */
    {% endif -%}
    {% if loop.index0 == 0 -%}
    @Id{% endif %}
    @Column(name = "{{item.columnName}}")
    private String {{item.columnName|replace(config.fieldPrefix, "")}};
    {% endfor %}
}
