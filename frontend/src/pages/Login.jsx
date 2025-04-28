import Form from "../components/Form"

function Login() {
    // return Form component with the necessary parameters
    return <Form route="/api/token/" method="login" />
}

export default Login