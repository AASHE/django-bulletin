/**
 * @jsx React.DOM
 */
'use strict';

var React = require('react/addons');

var Accordion = require('react-bootstrap/Accordion');
var Button = require('react-bootstrap/Button');
var ButtonGroup = require('react-bootstrap/ButtonGroup');
var Input = require('react-bootstrap/Input');
var Panel = require('react-bootstrap/Panel');


var SectionTemplateAddCategoryWidget = React.createClass({
  render: function() {

    var unsectionedCategorySelectOptions = [];

    this.props.unsectionedCategories.forEach(function(unsectionedCategory) {
      unsectionedCategorySelectOptions.push(
        <option value={unsectionedCategory.id}>
          {unsectionedCategory.fully_qualified_name}
        </option>
      );
    });

    var addCategoryPanel = (
      <Accordion>
        <Panel className="panel-collapse collapse in"
               expanded={false}
               id={"addCategoryPanel" + this.props.sectionTemplateId}
               header="Categories with no section">

          <Input
              type="select"
              multiple
              id={"unsectionedCategorySelect" + this.props.sectionTemplateId}>
            {unsectionedCategorySelectOptions}
          </Input>

          <ButtonGroup>
            <Button onClick={this.addCategories}>
              Add Category
            </Button>
            <Button >
              Cancel
            </Button>
          </ButtonGroup>
        </Panel>
      </Accordion>
    );

    return (addCategoryPanel);
  },

  addCategories: function() {
    var unsectionedCategorySelect = $("#unsectionedCategorySelect" +
                                      this.props.sectionTemplateId);
    var sectionTemplateId = this.props.sectionTemplateId;
    var url = (this.props.apiURL +
               '/section-template/' + sectionTemplateId +
               '/category');
    var updateState = this.props.updateState;

    unsectionedCategorySelect.val().forEach(function(categoryId) {
      $.ajax({
        url: url,
        type: 'POST',
        data: {category_id: categoryId},
        dataType: 'json',
        success: function(data) {
          // Here's a bug.  The next line deselects all selected
          // options in the selection of unsectioned categories.
          // Unfortunately, this happens for each item in
          // the list of selected categories. Should
          // only do for the option specified by categoryId here,
          // but this is beyond my Javascript-fu for now.
          unsectionedCategorySelect.val([]);
          updateState();
        }.bind(this),
        error: function(xhr, status, err) {
          alert("Something broke. " + err);
          console.error(url, status, err.toString());
        }.bind(this)
      });
    });
  }

});

module.exports = SectionTemplateAddCategoryWidget;
