{% set table = config.table|capitalize -%}
package jnpf.base.service.impl;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;
import jnpf.base.entity.{{table}}Entity;
import jnpf.base.mapper.{{table}}Mapper ;
import jnpf.base.service.{{table}}Service;
@Service
public class {{table}}ServiceImpl extends ServiceImpl<{{table}}Mapper, {{table}}Entity> implements {{table}}Service {
    
}
