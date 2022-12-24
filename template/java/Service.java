import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;

{% set table = config.table|capitalize %}
public interface {{table}}Service extends IService<{{table}}Entity> {
}
