/**
 * @jsx React.DOM
 */
var React = require('react/addons');
var Accordion = require('react-bootstrap/Accordion');
var Button = require('react-bootstrap/Button');
var Panel = require('react-bootstrap/Panel');

var SectionTemplateEditor = require('./SectionTemplateEditor');


var IssueTemplateEditor = React.createClass({
  render: function() {
    var sectionTemplateEditorListItems = [];
    var unsectionedCategories = this.props.unsectionedCategories;
    var updateState = this.props.updateState;
    var apiURL = this.props.apiURL;

    this.props.sectionTemplates.forEach(
      function(sectionTemplate) {
        sectionTemplateEditorListItems.push(
            <li>
              <SectionTemplateEditor
                  sectionTemplateName={sectionTemplate.name}
                  position={sectionTemplate.position}
                  categories={sectionTemplate.categories}
                  sectionTemplateId={sectionTemplate.id}
                  unsectionedCategories={unsectionedCategories}
                  key={sectionTemplate.id}
                  updateState={updateState}
                  apiURL={apiURL} />
            </li>
        );
      }
    );

    return (
      <Accordion>
        <Panel header={this.props.issueTemplateName}>
          <Button>
            New section
          </Button>
          <ul>
            {sectionTemplateEditorListItems}
          </ul>
        </Panel>
      </Accordion>
    );
  }
});

module.exports = IssueTemplateEditor;
