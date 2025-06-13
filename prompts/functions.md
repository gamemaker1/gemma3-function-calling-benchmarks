```function
{
	"name": "get_current_time",
	"description": "Returns the current time in ISO8601 format in the user's current timezone. Useful when the user provides a relative time and functions require an exact timestamp.",
	"parameters": {
		"type": "object",
		"properties": {},
		"required": []
	},
	"responses": [{
		"type": "object",
		"properties": {
			"timestamp": {
				"type": "string",
				"format": "date-time",
				"description": "Current time in ISO8601 format (e.g., '2024-03-15T14:30:45.123Z')"
			}
		}
	}],
	"examples": [{
		"description": "What is the time right now?",
		"parameters": {},
	}]
}
```

```function
  {
	"name": "get_weather_for_place",
	"description": "Retrieves the weather conditions for a place given the name of the place, the units to use, and the dates to fetch the weather for.",
	"parameters": {
		"type": "object",
		"properties": {
			"place": {
				"type": "string",
				"description": "The name of a place - could be a city name, unicode name of a location, area code or airport code. Do not assume a default and ask the user for the location."
			},
			"units": {
				"type": "string",
				"enum": ["metric", "uscs"]
				"description": "The units to use in the weather report. Defaults to metric."
			},
			"dates": {
				"type": "array",
				"items": {
					"type": "string",
					"format": "date",
					"description": "A date formatted as yyyy-mm-dd, for which the weather service will return its forecast. Defaults to a one-element array containing only today's date."
				}
			}
		},
		"required": ["place"]
	},
	"responses": [{
		"type": "array",
		"items": {
			"type": "object",
			"properties": {
				"temperature": {
					"type": "object",
					"properties": {
						"feels": {
							"type": "number",
							"description": "The temperature it feels like it is, in the specified units."
						},
						"actual": {
							"type": "number",
							"description": "The measured temperature, in the specified units."
						}
					}
				},
				"precipitation": {
					"type": "number",
					"description": "The forecasted rainfall, in inches or mm depending on the unit specified."
				},
				"uv": {
					"type": "number",
					"description": "The value of the UV index.",
				},
				"weather": {
					"type": "string",
					"description": "A short phrase describing the current weather in a user-friendly manner."
				}
			}
		}
	}],
	"errors": [{
		"name": "UnknownLocation",
		"description": "The location provided is not known to this weather service."
	}, {
		"name": "ServiceUnavailable",
		"description": "The weather service is currently down."
	}],
	"examples": [{
		"description": "What's the weather in Pune like right now?",
		"parameters": {
			"place": "Pune"
		}
	}]
}
```

```function
{
	"name": "get_user_info",
	"description": "Fetch's the current user's unique ID, along with their phone number and shipping address, given their e-mail address.",
	"parameters": {
	"type": "object",
		"properties": {
			"email": {
				"type": "string",
				"description": "The email address of the current user."
			}
		},
		"required": ["email"]
	},
	"responses": [{
		"type": "object",
		"properties": {
			"user_id": {
				"type": "string",
				"description": "The unique identifier for the user."
			},
      "shipping_address": {
          "type": "string",
          "description": "The new shipping address for the user."
      },
      "phone_number": {
          "type": "string",
          "description": "The new phone number for the user."
      }
		}
	}],
	"errors": [{
		"name": "UserNotFound",
		"description": "The user with the specified email address does not exist."
  }, {
		"name": "Forbidden",
		"description": "Forbidden to fetch user info for user not your own."
	}]
}
```

```function
{
    "name": "get_user_orders",
    "description": "Retrieves a list of orders for a given user ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The unique identifier for the user."
            },
            "status_filter": {
                "type": "string",
                "enum": ["pending", "shipped", "delivered", "cancelled"],
                "description": "Optional. Filters orders by a specific status."
            }
        },
        "required": ["user_id"]
    },
    "responses": [{
        "type": "object",
        "properties": {
            "orders": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "order_date": {"type": "string", "format": "date"},
                        "total_amount": {"type": "number"}
                    }
                }
            }
        }
    }],
    "errors": [{
        "name": "NoOrdersFound",
        "description": "The user has no orders, or no orders match the filter."
    }]
}
```

```function
{
    "name": "get_order_details",
    "description": "Gets the specific items and quantities for a single order.",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The unique identifier of the order."
            }
        },
        "required": ["order_id"]
    },
    "responses": [{
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"},
                        "quantity": {"type": "integer"}
                    }
                }
            }
        }
    }],
		"errors": [{
				"name": "OrderNotFound",
				"description": "Could not find order with the given ID."
		}]
}
```

```function
{
    "name": "get_product_info",
    "description": "Retrieves detailed information, like name and price, for a list of product IDs.",
    "parameters": {
        "type": "object",
        "properties": {
            "product_ids": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of unique product identifiers."
            }
        },
        "required": ["product_ids"]
    },
    "responses": [{
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string"},
                "product_name": {"type": "string"},
                "price": {"type": "number"}
            }
        }
    }],
		"errors": [{
				"name": "ProductNotFound",
				"description": "Could not find product with the given ID."
		}]
}
```

```function
{
    "name": "check_stock_and_add_to_cart",
    "description": "Checks if a product is in stock. If it is, adds the specified quantity to a user's cart.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "product_id": {"type": "string"},
            "quantity": {"type": "integer"}
        },
        "required": ["user_id", "product_id", "quantity"]
    },
    "responses": [{
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "message": {"type": "string", "description": "A confirmation or error message."}
        }
    }]
}
```

```function
{
    "name": "search_products",
    "description": "Searches for products based on a query. Can be filtered by category, price range, and sorted.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search term for the products."
            },
            "category": {
                "type": "string",
                "description": "Optional. The category to filter by (e.g., 'electronics', 'apparel')."
            },
            "min_price": {
                "type": "number",
                "description": "Optional. The minimum price for products to include."
            },
            "max_price": {
                "type": "number",
                "description": "Optional. The maximum price for products to include."
            },
            "sort_by": {
                "type": "string",
                "enum": ["relevance", "price_asc", "price_desc", "rating"],
                "description": "Optional. The order to sort the results. Defaults to 'relevance'."
            }
        },
        "required": ["query"]
    },
    "responses": [{
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string"},
                "product_name": {"type": "string"},
                "price": {"type": "number"}
            }
        }
    }]
}
```

```function
{
    "name": "update_user_profile",
    "description": "Updates a user's profile information. At least one updatable field must be provided.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The unique identifier for the user whose profile is to be updated."
            },
            "shipping_address": {
                "type": "string",
                "description": "The new shipping address for the user."
            },
            "phone_number": {
                "type": "string",
                "description": "The new phone number for the user."
            }
        },
        "required": ["user_id"]
    },
    "responses": [{
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "message": {"type": "string"}
        }
    }],
		"errors": [{
				"name": "Forbidden",
				"description": "This operation is forbidden."
		}]
}
```
