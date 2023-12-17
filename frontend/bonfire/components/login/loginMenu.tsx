import Logo from "../logo";
import LoginForm from "./loginForm";

const LoginMenu = () => {
    return(
        <div className="flex flex-col items-center gap-16">
            <div className="pl-5 scale-150">
                <Logo></Logo>
            </div>
            <LoginForm></LoginForm>
        </div>
    );
}

export default LoginMenu