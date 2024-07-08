package com.mockcompany.webapp.service;


import com.mockcompany.webapp.data.ProductItemRepository;
import com.mockcompany.webapp.model.ProductItem;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class SearchService {

    @Autowired
    ProductItemRepository productItemRepository;

    public List<ProductItem> searchAtServiceLevel(String query) {
        Iterable<ProductItem> productItem = productItemRepository.findAll();
        List<ProductItem> result = new ArrayList<>();
        boolean matchesFlag;

        for(ProductItem item : productItem) {
            String itemName = item.getName().toLowerCase();
            String queryName = query.toLowerCase();
            matchesFlag = itemName.contains(queryName);
            if(matchesFlag){
                result.add(item);
            }
        }
        return result;

    }


    public Map<String, Integer> searchProductCount(String... terms) {

        Map<String, Integer> results = new HashMap<>();
        for (String term : terms) {//from the terms like kids, cool, etc.
            long count = productItemRepository.countBySearchTerm(term);//then ge the count by the query terms
            results.put(term, (int) count);//casting to integer
        }
        return results;
    }
}
