package com.orangeslate.naturestore.test;

import java.util.ArrayList;

import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.orangeslate.naturestore.domain.User;
import com.orangeslate.naturestore.repository.PillBoxRepository;
import com.orangeslate.naturestore.repository.Repository;

@RestController
public class UserController {
	
	@RequestMapping("/start")
	public void start() {
		ConfigurableApplicationContext context = new ClassPathXmlApplicationContext(
				"classpath:/spring/applicationContext.xml");

		// Repository repository =
		// (Repository)context.getBean("natureRepository");

		Repository<User> repository = context.getBean(PillBoxRepository.class);

		// cleanup collection before insertion

//		
//		User(String id, String username, ArrayList<String> listeningTo,
//				ArrayList<String> heardBy, ArrayList<String> colorsRecieved, 
//				String colorSent)
		String idOne = "1";//UUID.randomUUID().toString();
		ArrayList<Integer> compartments = new ArrayList<Integer>();
		compartments.add(1);
		
		repository.save(new User(idOne, "Douglas", compartments));
		
		String idTwo = "2";//UUID.randomUUID().toString();
		compartments.add(2);
		compartments.add(4);
		
		repository.save(new User(idTwo, "Keith", compartments));
		
		String idThree = "3";//UUID.randomUUID().toString();
		compartments.add(5);
		
		repository.save(new User(idThree, "Carter", compartments));

		System.out.println("1. " + repository.getAll());
		
		System.out.println("Using Controller " + repository.getAll());
		
	}
	
	@RequestMapping("/user")
	public User user(@RequestParam(value="name", defaultValue="World") String name) {
		ConfigurableApplicationContext context = new ClassPathXmlApplicationContext(
				"classpath:/spring/applicationContext.xml");

		Repository<User> repository = context.getBean(PillBoxRepository.class);
		if(repository.getAll().size() > 0) {
			return repository.getAll().get(0);
		}
		else {
			return null;
		}
		
	}
}
