import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.lar.book.model.BookPage;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Mapper
@Repository
public interface {{config.table|capitalize}}Mapper extends BaseMapper<{{config.table|capitalize}}Entity> {
}