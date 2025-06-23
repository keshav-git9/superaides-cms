/**
 * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	 //config.language = 'fr';
	 config.allowedContent = true; // disables all filtering
     config.extraAllowedContent = 'span[*];section[*];div[*];*(*){*}'; // fine-grained control
     config.removePlugins = 'stylesheetparser';
	 config.uiColor = '#a7bdea';
	 config.toolbar = 'Custom';
	 config.toolbar_Custom =[       
		{ name: 'document', items: [ 'Source', '-', 'NewPage','-', 'Templates' ] },
        { name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord' ] },
        { name: 'editing', items : [ 'Find','Replace','-','SelectAll' ] },
								{ name: 'paragraph', items : [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-','JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
        { name: 'insert', items : [ 'Image','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ]},
								{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },  
								{ name: 'tools', items  : ['Maximize','-','About', 'ShowBlocks']},  
        { name: 'colors', items : ['TextColor', 'BGColor']},	
								{ name: 'styles', items : [ 'Styles', 'Format', 'Font', 'FontSize' ] },
        { name: 'basicstyles',groups: [ 'basicstyles', 'cleanup' ], items : [ 'Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat' ] },
		];
};
