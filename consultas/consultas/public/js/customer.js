frappe.ui.form.on("Customer", {
	"refresh": function(frm) {
		console.log("Completed");
		frm.set_df_property('tipo_rnc', 'options', [{
        		"value": "1",
        		"label": "RNC"
        	},
        	{
        		"value": "2",
        		"label": "CEDULA"
        	},
        ]);

        frm.page.show_menu();

		$.map(["edad", "gender"], function(field) {
			frm.toggle_reqd(field, frm.doc.customer_group == "Clientes");
		});

		$.map(["nss", "ars", "gender"], function(field) {
			frm.toggle_display(field, frm.doc.customer_group == "Clientes");
		});


		if (frm.doc.customer_group == "Clientes") {
			! frm.is_new() && frm.custom_buttons["Accounts Receivable"].hide()
		}

		frm.trigger("hide_dashboard");
	},
	onload: function(frm) {
        if (frm.is_new()) {
            frm.set_value("tipo_rnc", frm.doc.customer_group == "Clientes"? 2: 1);
        }
    },
	"onload_post_render": function(frm) {
		frm.set_query("ars", function(){
			return {
				"query": "erpnext.controllers.queries.customer_query",
				"filters": {
					"customer_group": "Proveedores"
				}
			};
		});
	},
	"customer_name": function(frm) {
		frm.set_value('customer_name', frm.doc.customer_name.trim().toUpperCase())
	},
	"tax_id": function(frm) {
		frm.set_value('tax_id', mask_ced_pas_rnc(frm.doc.tax_id.trim()))
	},
	"ars": function(frm) {
		frm.toggle_reqd("nss", !! frm.doc.ars);
	},
	customer_group: function(frm) {
        
        frm.set_value("tipo_rnc", frm.doc.customer_group == "Clientes"? 2: 1);

		var fields = ["nss", "ars", "gender", "edad"];

		$.map(fields, function(field) {
			frm.set_value(field, null);
		});

		frm.set_value("naming_series", frm.doc.customer_group == "Clientes" ? "CUST-":"PROV-")

		frm.trigger("refresh");
	},
	"hide_dashboard": function(frm) {
		frm.dashboard.wrapper.parent().addClass("hide")
			.parent().find(".section-head").addClass("collapsed")
			.find(".octicon.collapse-indicator.octicon-chevron-up")
			.removeClass()
			.addClass("octicon collapse-indicator octicon-chevron-down");
	},
	"validate": function(frm) {
		if (frm.doc.customer_group != "Clientes") {
			var fields = ["nss", "ars", "gender", "edad"];
			$.map(fields, function(field) {
				if (frm.doc[field]) {
					frappe.throw(__("Campo {0}: debe estar vacio si no es un cliente!",
						[cur_frm.fields_dict[field]._label]));
				}
			});
		}
	}
});

function mask_ced_pas_rnc(input) {
	input = input.trim().replace(/-/g,"")
	
	if (input.length == 11)
		return ("{0}{1}{2}-{3}{4}{5}{6}{7}{8}{9}-{10}".format(input));

	if (input.length == 9)
		return ("{0}-{1}{2}-{3}{4}{5}{6}{7}-{8}".format(input));
	
	return input
}

