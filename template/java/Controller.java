{% set table = config.table|capitalize -%}
{% set modelName = config.modelName -%}
package jnpf.base.controller;

import org.springframework.beans.factory.annotation.Autowired;
import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import jnpf.base.ActionResult;
import jnpf.base.entity.{{modelName}}Entity;
import jnpf.base.service.{{modelName}}Service;
import jnpf.util.RandomUtil;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import jnpf.base.model.{{config.table}}.{{modelName}}Info;
import jnpf.base.model.{{config.table}}.{{modelName}}Query;
@RestController
@RequestMapping("/{{config.table}}")
public class  {{modelName}}Controller {
    @Autowired
    private {{modelName}}Service {{config.table}}Service;
    /**
     * 获取列表
     * @param page
     * @return
     */
    @PostMapping("list")
    public ActionResult<?> list(@RequestBody @Validated {{modelName}}Query page) {
        QueryWrapper<{{modelName}}Entity> wrapper = new QueryWrapper<>();
        {% for item in config.searchList -%}
        if(page.get{{item|capitalize}}()!=null){
          wrapper.lambda().eq({{modelName}}Entity::get{{item|capitalize}}, page.get{{item|capitalize}}());
        }
        {% endfor %}
        
        {{modelName}}Query info = {{config.table}}Service.page(page, wrapper);
        
        return ActionResult.success(info);
    }
    /**
     * 查询信息 
     * @param id
     * @return
     */
    @GetMapping("/{id}")
    public ActionResult<?> info(@PathVariable String id) {

        {{modelName}}Entity info = {{config.table}}Service.getById(id);
        return ActionResult.success(info);
    }
    /**
     * 保存信息
     * @param info
     * @return
     */
    @PostMapping("save")
    public ActionResult<?> save(@RequestBody @Validated {{modelName}}Info info) {
        {{modelName}}Entity {{config.table}}Entity = BeanUtil.copyProperties(info, {{modelName}}Entity.class);
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
    public ActionResult<?> update(@RequestBody @Validated {{modelName}}Info info) {

        {{modelName}}Entity {{config.table}}Entity = BeanUtil.copyProperties(info, {{modelName}}Entity.class);
        {{config.table}}Service.updateById({{config.table}}Entity);
        return ActionResult.success("更新成功");
    }
    /**
     * 删除信息
     * @param id
     * @return
     */
    @DeleteMapping("/{id}")
    public ActionResult<?> delete(@PathVariable String id) {
        {{config.table}}Service.removeById(id);
        return ActionResult.success("删除成功");
    }

}
