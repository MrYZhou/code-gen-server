

import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
{% set table = config.table|capitalize %}
@RestController
@RequestMapping("/{{config.table}}")
public class  {{table}}Controller {
    @Autowired
    private {{table}}Service {{config.table}}Service;
    /**
     * 获取列表
     * @param page
     * @return
     */
    @PostMapping("list")
    public ActionResult<T> list(@RequestBody @Validated {{table}}Query page) {
        QueryWrapper<{{table}}Entity> wrapper = new QueryWrapper<>();
        {% for item in config.searchList -%}
        if(page.get{{item|capitalize}}()!=null){
          wrapper.lambda().eq({{table}}Entity::get{{item|capitalize}}, page.get{{item|capitalize}}());
        }
        {% endfor %}
        
        {{table}}Query info = {{config.table}}Service.page(page, wrapper);
        
        return ActionResult.success(info);
    }
    /**
     * 查询信息 
     * @param id
     * @return
     */
    @GetMapping("/{id}")
    public ActionResult<T> info(@PathVariable String id) {

        {{table}}Entity info = {{config.table}}Service.getById(id);
        return ActionResult.success(info);
    }
    /**
     * 保存信息
     * @param info
     * @return
     */
    @PostMapping("save")
    public ActionResult<T> save(@RequestBody @Validated {{table}}Info info) {
        {{table}}Entity {{config.table}}Entity = BeanUtil.copyProperties(info, {{table}}Entity.class);
        {{config.table}}Entity.setId(RandomUtil.uuId());
        {{config.table}}Service.save({{config.table}}Entity);
        return ActionResult.success("保存成功");
    }
    /**
     * 更新信息
     * @param info
     * @return
     */
    @PutMapping("update")
    public ActionResult<T> update(@RequestBody @Validated {{table}}Info info) {

        {{table}}Entity {{config.table}}Entity = BeanUtil.copyProperties(info, {{table}}Entity.class);
        {{config.table}}Service.updateById({{config.table}}Entity);
        return ActionResult.success("更新成功");
    }
    /**
     * 删除信息
     * @param id
     * @return
     */
    @DeleteMapping("/{id}")
    public ActionResult<T> delete(@PathVariable String id) {
        {{config.table}}Service.removeById(id);
        return ActionResult.success("删除成功");
    }

    // @GetMapping("excel")
    // public void download(HttpServletResponse response) throws IOException {
    //     response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
    //     response.setCharacterEncoding("utf-8");
    //     String fileName = "test";
    //     response.setHeader("Content-disposition", "attachment;filename*=utf-8''" + fileName + ".xlsx");

    //     List<{{table}}Entity> list = {{config.table}}Service.list();

    //     EasyExcel.write(response.getOutputStream(), {{table}}Entity.class).sheet("数据").doWrite(list);
    // }

    // @PostMapping("excel")
    // @ResponseBody
    // public ActionResult<T> upload(@RequestPart("file") MultipartFile file) throws IOException {
    //     EasyExcel.read(file.getInputStream(), {{table}}Entity.class, new PageReadListener<{{table}}Entity>(
    //             {{config.table}}Service::saveBatch)).sheet().doRead();
    //     return ActionResult.success();
    // }

  

}
