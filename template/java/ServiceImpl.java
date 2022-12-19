import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.lar.{{table}}.model.{{table}}Page;
import org.springframework.stereotype.Service;

import java.util.List;
{% set table = config.table|capitalize %}
@Service
public class {{table}}ServiceImpl extends ServiceImpl<{{table}}Mapper, {{table}}Entity> implements {{table}}Service {
    
}
