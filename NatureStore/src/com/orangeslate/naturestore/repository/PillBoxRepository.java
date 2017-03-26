package com.orangeslate.naturestore.repository;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

import com.mongodb.WriteResult;
//import com.orangeslate.naturestore.domain.Tree;
import com.orangeslate.naturestore.domain.User;

public class PillBoxRepository implements Repository<User> {

	MongoTemplate mongoTemplate;
	
	public void setMongoTemplate(MongoTemplate mongoTemplate) {
		this.mongoTemplate = mongoTemplate;
	}
	
	@Override
	public List<User> getAll() {
		return mongoTemplate.findAll(User.class);
	}

	@Override
	public void save(User user) {
		mongoTemplate.insert(user);
	}

	@Override
	public User get(String id) {
		return mongoTemplate.findOne(new Query(Criteria.where("id").is(id)),
				User.class);
	}

	@Override
	public WriteResult update(String id, String name) {
		return mongoTemplate.updateFirst(
				new Query(Criteria.where("id").is(id)),
				Update.update("name", name), User.class);
	}
	
	@Override
	public WriteResult updateCompartments(String id, ArrayList<Integer> compartments) {
		return mongoTemplate.updateFirst(
				new Query(Criteria.where("id").is(id)),
				Update.update("name", compartments.toArray()), User.class);
	}
	
	@Override
	public void delete(String id) {
		mongoTemplate
		.remove(new Query(Criteria.where("id").is(id)), User.class);
		
	}

	@Override
	public void createCollection() {
		if (!mongoTemplate.collectionExists(User.class)) {
			mongoTemplate.createCollection(User.class);
		}
		
	}

	@Override
	public void dropCollection() {
		// TODO Auto-generated method stub
		if (mongoTemplate.collectionExists(User.class)) {
			mongoTemplate.dropCollection(User.class);
		}
	}

	
}
