{% set table = config.table|capitalize -%}
{% set modelName = config.modelName -%}
package jnpf.base.service;
import com.baomidou.mybatisplus.extension.service.IService;
import jnpf.base.entity.{{modelName}}Entity;


public interface {{modelName}}Service extends IService<{{modelName}}Entity> {
}
