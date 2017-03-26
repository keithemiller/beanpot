package com.orangeslate.naturestore.domain;

import java.util.ArrayList;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

public class User {
	@Id
	private String id;

	private String name;
	
	private ArrayList<Integer> compartments;

	public User(String id, String name, ArrayList<Integer> compartments) {
		this.id = id;
		this.name = name;
		this.setCompartments(compartments);
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setUsername(String name) {
		this.name = name;
	}

	public ArrayList<Integer> getCompartments() {
		return compartments;
	}

	public void setCompartments(ArrayList<Integer> compartments) {
		this.compartments = compartments;
	}
	

//	private String id;
//	private String username;
//	private ArrayList<String> listeningTo;
//	private ArrayList<String> heardBy;
//	private ArrayList<String> colorsRecieved;
//	private String colorSent;
	
	@Override
	public String toString() {
		return "Person [id=" + id + ", name=" + name + ", compartments" + compartments + "]";
	}
	
}
