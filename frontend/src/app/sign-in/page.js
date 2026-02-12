import { LoginForm } from "@/features/auth/components/LoginForm";
import AuthLayout from "@/layouts/AuthLayout";

export default function SignIn() {
  return (
    <AuthLayout>
      <LoginForm />
    </AuthLayout>
  );
}

