import { RegisterForm } from "@/components/sign-up/SignUpForm";
import AuthLayout from "@/layouts/AuthLayout";

export default function SignUp() {
  return (
    <AuthLayout>
      <RegisterForm />
    </AuthLayout>
  );
}

