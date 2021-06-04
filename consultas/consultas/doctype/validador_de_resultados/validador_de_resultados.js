// Copyright (c) 2020, Lewin Villar and contributors
// For license information, please see license.txt

frappe.ui.form.on('Validador de Resultados', {
	refresh: function(frm) {
		frm.disable_save();
		frm.page.set_primary_action(__("Validar Documentos"), function() {
			frm.call("validate_docs");
		});
		frappe.realtime.on("validator_progress", function(data) {
			if(data.progress) {
				frappe.hide_msgprint(true);
				frappe.show_progress(
					`Validating Documents`,
					data.progress[0],
					data.progress[1],
					data.progress[2]
				);

				if (data.progress[0] == data.progress[1])
					setTimeout(function() {frappe.hide_progress()}, 700);
			}
		});
	},
});
