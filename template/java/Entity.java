package com.lar.main.plan;

import lombok.Data;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Table(name = "plan")
@Entity
@Data
public class PlanEntity {
    @Id
    @Column(name = "id")
    private String id;
    @Column(name = "name")
    private String name;
}
