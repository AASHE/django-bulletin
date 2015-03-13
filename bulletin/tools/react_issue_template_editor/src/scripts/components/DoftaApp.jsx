/**
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');

var Accordion = require('react-bootstrap/Accordion');
var Button = require('react-bootstrap/Button');
var ButtonGroup = require('react-bootstrap/ButtonGroup');
var Input = require('react-bootstrap/Input');
var Modal = require('react-bootstrap/Modal');
var ModalTrigger = require('react-bootstrap/ModalTrigger');
var Panel = require('react-bootstrap/Panel');
var Glyphicon = require('react-bootstrap/Glyphicon');

var IssueTemplateEditor = require('./IssueTemplateEditor');

// Export React so the devtools can find it
(window !== window.top ? window.top : window).React = React;

// CSS
require('../../styles/reset.css');
require('../../styles/main.css');


var DoftaApp = React.createClass({
  render: function() {
    return (
      <IssueTemplateEditor issueTemplateName={this.state.issueTemplateName}
                           sectionTemplates={this.state.sectionTemplates}
                           unsectionedCategories={this.state.unsectionedCategories}
                           updateState={this.updateState}
                           apiURL={this.props.apiURL}  />
    );
  },

  loadIssueTemplateFromServer: function() {
    $.ajax({
      url: (this.props.apiURL +
            '/issue-template/' +
            this.props.issueTemplateID),
      dataType: 'json',
      success: function(data) {
        this.setState({issueTemplateName: data.name});
        this.setState({sectionTemplates: data.section_templates});
      }.bind(this),
      error: function(xhr, status, err) {
        alert("Something broke. " + err);
        console.error(url, status, err.toString());
      }.bind(this)
    });
  },

  loadUnsectionedCategoriesFromServer: function() {
    $.ajax({
      url: this.props.apiURL + '/category',
      dataType: 'json',
      success: function(data) {
        var unsectionedCategories = data.filter(
          function (category) {
            return (category.section_templates.length === 0);
          }
        );
        this.setState({unsectionedCategories: unsectionedCategories});
      }.bind(this),
      error: function(xhr, status, err) {
        alert(status, err.toString());
        console.error(status, err.toString());
      }.bind(this)
    });
  },

  updateState: function() {
    this.loadIssueTemplateFromServer();
    this.loadUnsectionedCategoriesFromServer();
  },

  componentDidMount: function() {
    this.updateState();
  },

  getInitialState: function() {
    return (
      {issueTemplateName: '',
       sectionTemplates: [],
       unsectionedCategories: []}
    );
  }
});

React.renderComponent(
    <DoftaApp apiURL="http://localhost:7000/newsletter/api"
              issueTemplateID={2} />,
    document.getElementById('content')
);

module.exports = DoftaApp;
