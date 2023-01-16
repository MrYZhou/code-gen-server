package jnpf.base.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;
import jnpf.base.entity.{{config.table|capitalize}}Entity;

@Mapper
@Repository
public interface {{config.table|capitalize}}Mapper extends BaseMapper<{{config.table|capitalize}}Entity> {
}