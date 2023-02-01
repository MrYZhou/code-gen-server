{% set modelName = config.modelName -%}
package jnpf.base.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import jnpf.base.entity.{{modelName}}Entity;

@Mapper
@Repository
public interface {{modelName}}Mapper extends BaseMapper<{{modelName}}Entity> {
}