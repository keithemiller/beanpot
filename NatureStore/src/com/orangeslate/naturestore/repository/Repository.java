package com.orangeslate.naturestore.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

import com.mongodb.WriteResult;
import com.orangeslate.naturestore.domain.User;

public interface Repository<a> {

	public List<a> getAll();

	public void save(a tree);

	public a get(String id);

	public WriteResult update(String id, String name);
	
	public WriteResult updateCompartments(String id, ArrayList<Integer> compartments);
	
	public void delete(String id);

	public void createCollection();

	public void dropCollection();
}
