package com.lar.main.plan;

import com.lar.main.plan.model.PlanQuery;
import org.springframework.data.domain.Page;

import java.util.List;

public interface PlanService {

    List findAll();

    Page<PlanEntity> page(PlanQuery query);
}
