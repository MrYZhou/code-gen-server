{% set table = config.table|capitalize -%}
package jnpf.base.service;
import com.baomidou.mybatisplus.extension.service.IService;
import jnpf.base.entity.{{table}}Entity;


public interface {{table}}Service extends IService<{{table}}Entity> {
}
