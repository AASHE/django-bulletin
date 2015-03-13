/**
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var Accordion = require('react-bootstrap/Accordion');
var Button = require('react-bootstrap/Button');
var Input = require('react-bootstrap/Input');
var Panel = require('react-bootstrap/Panel');

var SectionTemplateAddCategoryWidget = require(
  './SectionTemplateAddCategoryWidget');

var SectionTemplateEditor = React.createClass({
  render: function() {
    var categorySelectOptions = [];

    this.props.categories.forEach(function(category) {
      categorySelectOptions.push(
          <option value={category.id}>
            {category.fully_qualified_name}
          </option>
      );
    });

    return (
      <Accordion>
        <Panel header={this.props.sectionTemplateName}>
          <Input type="select"
                 multiple
                 id={"sectionTemplateCategorySelect" +
                     this.props.sectionTemplateId}>
            {categorySelectOptions}
          </Input>
          <Button onClick={this.removeCategoriesFromSectionTemplate}>
            Remove category
          </Button>
          <SectionTemplateAddCategoryWidget
            unsectionedCategories={this.props.unsectionedCategories}
            sectionTemplateId={this.props.sectionTemplateId}
            updateState={this.props.updateState}
            apiURL={this.props.apiURL} />
        </Panel>
      </Accordion>
    );
  },

  removeCategoriesFromSectionTemplate: function() {
    var sectionTemplateCategorySelect = $("#sectionTemplateCategorySelect" +
                                          this.props.sectionTemplateId);
    var sectionTemplateId = this.props.sectionTemplateId;
    var categoryId = this.props.categoryId;
    var updateState = this.props.updateState;
    /*
     Why do I have to do that?  Declare variables and pull in values
     from this.props for them?  Because this.props isn't defined within
     the forEach function below -- why is that?  Why isn't this.props
     available down there, but these variables are?
     */
    if (sectionTemplateCategorySelect.val()) {
      sectionTemplateCategorySelect.val().forEach(function(categoryId) {

        var url = (this.props.apiURL +
                   '/section-template/' + sectionTemplateId +
                   '/category/' + categoryId);

        $.ajax({
          url: url,
          type: 'DELETE',
          dataType: 'json',
          success: function(data) {
            // Yes, this should't happen for every selected category,
            // see the comment in IssueTemplateEditor.addCategories.
            // But it's cheap, right?  I can't even see a flicker.
            sectionTemplateCategorySelect.val([]);
            updateState();
          }.bind(this),
          error: function(xhr, status, err) {
            alert("Something broke. " + err);
            console.error(status, err.toString());
          }.bind(this)
        });
      });
    }
  },

  getDefaultProps: function() {
    return ({'categories': []});
  }
});

module.exports = SectionTemplateEditor;
