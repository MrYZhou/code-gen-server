{% set table = config.table|capitalize -%}
{% set modelName = config.modelName -%}
package jnpf.base.service.impl;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;
import jnpf.base.entity.{{modelName}}Entity;
import jnpf.base.mapper.{{modelName}}Mapper ;
import jnpf.base.service.{{modelName}}Service;
@Service
public class {{modelName}}ServiceImpl extends ServiceImpl<{{modelName}}Mapper, {{modelName}}Entity> implements {{modelName}}Service {
    
}
