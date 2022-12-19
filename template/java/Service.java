import com.baomidou.mybatisplus.extension.service.IService;
import com.lar.{{table}}.model.{{table}}Page;

import java.util.List;

{% set table = config.table|capitalize %}
public interface {{table}}Service extends IService<{{table}}Entity> {
}
