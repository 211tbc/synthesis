dataSource {
	pooled = true
	driverClassName = "org.postgresql.Driver"
	username = "synthesis"
	password = "synthesis"
}
hibernate {
    cache.use_second_level_cache=true
    cache.use_query_cache=true
    cache.provider_class='com.opensymphony.oscache.hibernate.OSCacheProvider'
    show_sql=true
}
// environment specific settings
environments {
	development {
		dataSource {
			// dbCreate = "update" // one of 'create', 'create-drop','update'
			url = "jdbc:postgresql://gadget/synthesis_trunk"
		}
	}
	test {
		dataSource {
			dbCreate = "update"
			url = "jdbc:hsqldb:mem:testDb"
		}
	}
	production {
		dataSource {
			dbCreate = "update"
			url = "jdbc:hsqldb:file:prodDb;shutdown=true"
		}
	}
}