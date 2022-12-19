

import cn.hutool.core.bean.BeanUtil;
import com.alibaba.excel.EasyExcel;
import com.alibaba.excel.read.listener.PageReadListener;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.lar.book.model.{{table}}Info;
import com.lar.book.model.BookPage;
import common.base.AppResult;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
{% set table = config.table|capitalize %}
@RestController
@RequestMapping("/{{config.table}}")
public class BookController {
    @Autowired
    private final {{table}}Service {{config.table}}Service;
    /**
     * 获取列表
     * @param page
     * @return
     */
    @PostMapping("list")
    public AppResult<Object> list(@RequestBody @Validated {{table}}Query page) {
        QueryWrapper<{{table}}Entity> wrapper = new QueryWrapper<>();
        {% for item in config.searchList -%}
        if(page.get{{item|capitalize}}()!=null){
          wrapper.lambda().eq({{table}}Entity::get{{item|capitalize}}, page.get{{item|capitalize}}());
        }
        {% endfor %}
        
        {{table}}Query info = {{config.table}}Service.page(page, wrapper);
        
        return AppResult.success(info);
    }
    /**
     * 查询信息 
     * @param id
     * @return
     */
    @GetMapping("/{id}")
    public AppResult<Object> info(@PathVariable String id) {

        {{table}}Entity info = {{config.table}}Service.getById(id);
        return AppResult.success(info);
    }
    /**
     * 保存信息
     * @param info
     * @return
     */
    @PostMapping
    public AppResult<Object> save(@RequestBody @Validated {{table}}Info info) {
        {{table}}Entity {{config.table}}Entity = BeanUtil.copyProperties(info, {{table}}Entity.class);
        {{config.table}}Service.save({{table}}Entity);
        return AppResult.success();
    }
    /**
     * 修改信息
     * @param info
     * @return
     */
    @PutMapping
    public AppResult<Object> update(@RequestBody @Validated {{table}}Info info) {

        {{table}}Entity {{config.table}}Entity = BeanUtil.copyProperties(info, {{table}}Entity.class);
        {{config.table}}Service.updateById({{table}}Entity);
        return AppResult.success();
    }
    /**
     * 删除信息
     * @param id
     * @return
     */
    @DeleteMapping("/{id}")
    public AppResult<Object> delete(@PathVariable String id) {
        boolean b = {{config.table}}Service.removeById(id);
        return AppResult.success(b);
    }

    @GetMapping("excel")
    public void download(HttpServletResponse response) throws IOException {
        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        String fileName = "test";
        response.setHeader("Content-disposition", "attachment;filename*=utf-8''" + fileName + ".xlsx");

        List<{{table}}Entity> list = {{config.table}}Service.list();

        EasyExcel.write(response.getOutputStream(), {{table}}Entity.class).sheet("数据").doWrite(list);
    }

    @PostMapping("excel")
    @ResponseBody
    public AppResult<Object> upload(@RequestPart("file") MultipartFile file) throws IOException {
        EasyExcel.read(file.getInputStream(), {{table}}Entity.class, new PageReadListener<{{table}}Entity>(
                {{config.table}}Service::saveBatch)).sheet().doRead();
        return AppResult.success();
    }

  

}
