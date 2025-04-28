import Form from "../components/Form"

function Register() {
    // return Form component with the necessary parameters
    return <Form route="/api/user/register/" method="register" />
}

export default Register