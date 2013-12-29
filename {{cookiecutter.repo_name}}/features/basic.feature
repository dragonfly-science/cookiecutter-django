
Feature: Access {{ cookiecutter.domain_name }}

  Scenario: Download the base url of {{ cookiecutter.domain_name }}

    Given the url "http://{{ cookiecutter.domain_name }}"
    When I fetch this url
    Then the reponse is 200


