var app = {};

var Router = Backbone.Router.extend({

	routes : {
		"" : "people",
		"show/:id" : "show",
		"logreg" : "logreg",
		"login" : "login",
		"register" : "register",
		"profile/:id" : "profile"
	},

	cleanup : function() {
		if(!app.coreView) {
			app.coreView = new CoreView();
			app.mapView = new MapView();
			return true;
		}
		return false;
	},

	removeAll : function() {
		if(app.personView) app.personView.destroy(); app.personView = null;
		if(app.profileView) app.profileView.destroy(); app.profileView = null;
		if(app.peopleView) app.peopleView.hide();
	},



	people : function() {
		this.removeAll();
		this.cleanup();
		app.peopleView || (app.peopleView = new PeopleView());
		app.peopleView.show();
	},

	show : function(id) {
		this.removeAll();
		this.cleanup();
		app.personView = new PersonView({model : new Person({id : id})})
	},


	logreg : function() {
		if(this.cleanup()) {
			app.peopleView = new PeopleView();

		}
		$('#login-modal').modal('show');
	},

	profile : function(id) {
		this.removeAll();

		this.cleanup();
		app.profileView = new ProfileView({model : new Profile({id : id})})
	}

});


var Person = Backbone.Model.extend({

	initialize : function(opts) {
		this.attributes = opts;
	},

	url : function() {
		return '/api/people/'+this.get('id')

	}, 

	parse : function(resp) {
		return resp.person;
	}
});

var Profile = Backbone.Model.extend({
	url : function() {
		return '/api/profile/'+this.get('id');
	}
});

var Karma = Backbone.Model.extend({

	initialize : function() {
	},

	url : function() {
		return '/api/people/'+this.get('person')+'/karma'
	},

	parse : function(resp) {
		return resp.karma
	}
});

var Flag = Backbone.Model.extend({

	initialize : function() {
	},

	url : function() {
		return '/api/people/'+this.get('person')+'/flags';
	},

	parse : function(resp) {
		return resp.flags
	}
});


var People = Backbone.Collection.extend({

	initialize : function(opts) {
	},

	url : function() {
		return '/api/people'
	},


	parse : function(resp) {
		return resp.people;
	},

	comparator : function(obj1, obj2) {
		return obj1.get('name') > obj2.get('name')? 1 : -1	
	}

});


var ProfileView = Backbone.View.extend({

	el : '#profile',

	events : {
		'click #add-service-btn' : 'addService',
		'click .removeService' : 'removeService',
		'click .save-btn' : 'save',
		'keyup .saveable' : 'onKey',
		'click .label-pressable' : 'contactWhen'
	},

	fields : ['name', 'description', 'phone', 'email', 'beer'],

	initialize : function(opts) {
		this.model = opts.model;
		this.template = _.template($('#profile-view').html());
		this.saveable = false;
		this.load();
		var self = this;
		this.listenTo(this.model, "sync", function(model, resp, opts) {
			this.saveable = false;
			self.render(resp.errors)
		});
		if(app.peopleView) {
			app.peopleView.clear();
		}
		_.bindAll(this, 'onMarkerMoved');
	},

	load : function() {
		var self = this;
		this.model.fetch({
			success : function(model) {
				self.render();
			}, 

			error : function() {

			}
		});
	},

	render : function(errors) {
		var obj = this.model.toJSON();
		obj.person.errors = errors
		var profile = this.template(obj);
		this.$el.html(profile);


		//Kill the old one
		if(this.model.marker) {
			this.model.marker.setMap(null);
		}
		var p = this.model.get('person');
		var marker = app.mapView.createMarker(p.lat, p.lng, p.name);
		marker.setDraggable(true);		
		this.model.marker = marker;
		google.maps.event.addListener(marker, 'dragend', this.onMarkerMoved);
		app.mapView.center(marker);
		this.renderSave();

		this.$el.show();
	},

	onMarkerMoved : function() {
		var latlng = this.model.marker.getPosition();
		var lat = latlng.lat();
		var lng = latlng.lng();
		this.model.get('person').lat = lat;
		this.model.get('person').lng = lng;
		this.allowSave();
		this.renderSave();
	},

	addService : function() {
		var srv = $('#add-service-select').val();
		if(!_.find(this.model.get('person').services, function(obj) {
			return obj.name === srv;
		})) {
			this.allowSave();
			this.model.get('person').services.push({name : srv});
			this.render();
		}
	},

	removeService : function(e) {
		this.allowSave();
		var srv = $(e.currentTarget).attr('data-service');
		this.model.get('person').services = _.filter(
			this.model.get('person').services, function(obj) {
			return obj.name != srv
		});
		this.render();
	},

	onKey : function(e) {
		var $el = $(e.currentTarget);
		this.model.get('person')[$el.attr('id')] = $el.val();
		this.allowSave();
		this.renderSave();
	},

	contactWhen : function(e) {
		this.model.get('person').ok_contact = $(e.currentTarget).attr('data-val');
		this.allowSave();
		this.render();
	},

	allowSave : function() {
		this.saveable = true;
		window.onbeforeunload = function() {
			return "You have changes you have not saved yet. Are you sure you want to discard them?";
		}

	},

	renderSave : function() {
		if(this.saveable) {
			$('.save-btn').removeClass('disabled');
		} else {
			$('.save-btn').addClass('disabled');
		}
	},

	save : function() {
		if(!this.saveable) {
			return;
		}
		var self = this;
		this.$el.find('.saveable').each(function(i, obj) {
			self.model.get('person')[$(obj).attr('id')] = $(obj).val();
		});
		this.model.sync('update', this.model);
		window.onbeforeunload = null;
	}, 

	
	destroy : function() {
		this.$el.hide();
		this.unbind();
		this.$el.html('');
		this.undelegateEvents();
		this.model.marker.setMap(null);
	},

})


var PersonView = Backbone.View.extend({

	initialize : function() {

	},

	events : {
		'click #karma-btn' : 'karma',
		'click #flag-btn' : 'flag',
		'click #submit-karma' : 'submitKarma',
		'click #submit-flag' : 'submitFlag',
		'click .cancel-person-action' : 'cancelPersonAction'
	},

	el : '#person',
	model : Person,

	initialize : function(opts) {

		this.model = opts.model;
		this.template = _.template($('#person-view').html());
		this.load();
	},

	load : function() {
		var self = this;
		this.model.fetch({
			success : function(model) {
				self.render();
			}, 

			error : function() {

			}
		})
	},

	render : function() {
		var person = this.template(this.model.toJSON());
		if(this.model.marker) {
			this.model.marker.setMap(null);
		}
		var marker = app.mapView.createMarker(this.model.get('lat'), this.model.get('lng'), this.model.get('name'));
		this.model.marker = marker;
		app.mapView.center(marker);
		this.$el.html(person);
		this.$el.height($('#map-canvas').height());
		this.$el.show();
	},

	destroy : function() {
		this.$el.hide();
		this.unbind();
		this.$el.html('');
		this.undelegateEvents();
		this.model.marker.setMap(null);
	},


	karma : function() {
		this.cancelPersonAction();
		$('#karma-form').fadeIn(250);

	},

	submitKarma : function() {
		var self = this;
		var data = {person : this.model.get('id'), description : $('#karma-text').val()};
		var k = new Karma(data);
		k.sync('create', k, {
			success : function() {
				self.load();
			},

			error : function() {
				console.log("error");
			}
		});
	},
	
	flag : function() {
		this.cancelPersonAction();
		$('#flag-form').fadeIn(250);
	},

	submitFlag : function() {
		var self = this;
		var data = {person : this.model.get('id'), description : $('#flag-text').val()};
		console.log(data);
		var f = new Flag(data);
		console.log(f.url());
		f.sync('create', f, {
			success : function() {
				self.load();
			},

			error : function() {
				console.log("error");
			}
		});
	},

	cancelPersonAction : function() {
		$('.person-action').hide();
	}

});


var MapView = Backbone.View.extend({

	initialize : function(opts) {
		var mapOpts = {
			center: new google.maps.LatLng(0, 0),
			zoom: 2,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		$('#map-canvas').height(Math.max($(window).height() - 140, 500));
		this.map = new google.maps.Map($("#map-canvas")[0], mapOpts);
	}, 

	createMarker : function(lat, lng, name) {
		var latlng = new google.maps.LatLng(lat, lng)
		var marker = new google.maps.Marker({
			position : latlng,
			title : name
		})
		marker.setMap(app.mapView.map);
		return marker;
	}, 

	cluster : function(markers) {
		this.markerCluster = new MarkerClusterer(this.map, markers);
	},

	clear : function() {
		if(this.markerCluster) this.markerCluster.clearMarkers();
	},

	center : function(marker) {
		this.map.setCenter(marker.getPosition());
		this.map.setZoom(12);
	}

})


var PeopleView = Backbone.View.extend({

	el : '#people-list',

	events : {
		'keyup #search-people' : "renderList"
	},

	template : _.template($('#people-list-view').html()),

	initialize : function(opts) {
		this.people = new People();
		this.load();

	},

	show : function() {
		this.$el.show();
		this.render();
	},

	hide : function() {
		this.$el.hide();
		this.clear();
	},


	load : function() {
		var self = this;
		this.people.fetch({
			success : function(collection, resp, opts) {

				self.render();
			}, 

			error : function() {

			}
		});
	},

	plot : function() {
		var self = this;
		var marks = []
		this.people.each(function(obj) {
			var marker = app.mapView.createMarker(obj.get('lat'), obj.get('lng'), obj.get('name'))
			obj.marker = marker;
			marks.push(marker);
			google.maps.event.addListener(marker, 'click', function() {
				app.router.navigate('/show/'+obj.id, {trigger : true});
			});
		});
		app.mapView.cluster(marks);
	},

	clear : function() {
		app.mapView.clear();
	},

	render : function() {
		this.clear();
		this.plot();
		this.renderList();

	},

	destroy : function() {
		this.$el.hide();
		this.$el.find('#people-list-inner').html('');
		this.clear();
		this.unbind();
		this.undelegateEvents();
	},


	renderList : function() {
		var records = this.applyFilters();
		var $inner = $('#people-list-inner');
		$inner.html(this.template({people : records.toJSON()}));
		this.$el.show();
		this.$el.height($('#map-canvas').height()-($('#people-list-controls').height()+38));
	},


	applyFilters : function() {
		var val = $('#search-people').val();
		var regex = new RegExp('.*'+val+'.*', 'i');
		if(val && val.length > 0) {
			vals = this.people.filter(function(obj) {
				if(regex.exec(obj.get('name'))) return true;
				if(regex.exec(obj.get('username'))) return true;
				if(regex.exec(obj.get('address'))) return true;
				if(regex.exec(obj.get('phone'))) return true;
				if(regex.exec(obj.get('description'))) return true;
				if(regex.exec(obj.get('email'))) return true;
				return false;
			});
			return new People(vals);
		}
		return this.people;
	},

});


var CoreView = Backbone.View.extend({

	events : {
		'click #login-btn' : 'login',
		'click #register-btn' : 'register'
	},
	el : 'body',

	initialize : function() {

	},


	register : function(e) {
		var $el = $(e.currentTarget);
		if($el.hasClass('disabled')) {
			return;
		}
		var $form = $('#register');
		var data = $form.serialize(true);
		$el.addClass('disabled');
		$.post('/register', data).success(function(resp) {
			$form.parent().html(resp);
		}).error(function(resp) {
			$el.removeClass('disabled');
			$form.parent().html(resp.responseText);
		});
	},

	login : function(e) {
		var $el = $(e.currentTarget);
		if($el.hasClass('disabled')) {
			return;
		}
		var $form = $('#login');
		var data = $form.serialize(true);
		$el.addClass('disabled');
		$.post('/login', data).success(function(resp) {
			$form.parent().html(resp);
			window.location = "/"
		}).error(function(resp) {
			$el.removeClass('disabled');
			$form.parent().html(resp.responseText);
			
		});
	},

});


$(document).ready(function() {
	app.router = new Router();
	Backbone.history.start();
});