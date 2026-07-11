import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { loginSuccess } from "@/store/slices/authSlice";
import { authService } from "@/services/auth.service";
import Button from "@/components/common/Button";
import Input from "@/components/common/Input";
import Card from "@/components/common/Card";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginFormData = z.infer<typeof loginSchema>;

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await authService.login(data);
      dispatch(loginSuccess(response));
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary-600 mb-2">ITSM</h1>
          <p className="text-secondary-600">Management System</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-danger-100 border border-danger-300 rounded-md">
            <p className="text-danger-800 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Input
            label="Email"
            type="email"
            placeholder="your@email.com"
            {...register("email")}
            error={errors.email?.message}
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            {...register("password")}
            error={errors.password?.message}
          />

          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
          >
            Sign In
          </Button>
        </form>

        <div className="mt-6 pt-6 border-t border-secondary-200">
          <p className="text-center text-sm text-secondary-600">
            Demo credentials:
            <br />
            Email: admin@example.com
            <br />
            Password: password123
          </p>
        </div>
      </Card>
    </div>
  );
};

export default LoginPage;
