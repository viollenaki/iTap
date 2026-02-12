import { RegisterForm } from "@/features/auth/components/RegisterForm";
import AuthLayout from "@/layouts/AuthLayout";

export default function SignUp() {
  return (
    <AuthLayout>
      <RegisterForm />
    </AuthLayout>
  );
}

