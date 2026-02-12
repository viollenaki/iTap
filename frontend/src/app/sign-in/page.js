import { LoginForm } from "@/components/sign-in/SignInForm";
import AuthLayout from "@/layouts/AuthLayout";

export default function SignIn() {
  return (
    <AuthLayout>
      <LoginForm />
    </AuthLayout>
  );
}

