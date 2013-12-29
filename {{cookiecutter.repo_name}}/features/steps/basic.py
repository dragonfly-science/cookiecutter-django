
from behave import given, when, then

@given(u'the url "{url}"')
def step_impl(context, url):
    assert False

@when(u'I fetch this url')
def step_impl(context):
    assert False

@then(u'the reponse is 200')
def step_impl(context):
    assert False

