import React from "react";
import { render, screen } from "../utils/testUtils";
import Button from "@/components/common/Button";

describe("Button Component", () => {
  it("renders button with text", () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole("button", { name: /click me/i });
    expect(button).toBeInTheDocument();
  });

  it("renders button with primary variant", () => {
    render(<Button variant="primary">Primary</Button>);
    const button = screen.getByRole("button", { name: /primary/i });
    expect(button).toHaveClass("bg-primary-600");
  });

  it("renders button with secondary variant", () => {
    render(<Button variant="secondary">Secondary</Button>);
    const button = screen.getByRole("button", { name: /secondary/i });
    expect(button).toHaveClass("bg-secondary-200");
  });

  it("renders button with danger variant", () => {
    render(<Button variant="danger">Delete</Button>);
    const button = screen.getByRole("button", { name: /delete/i });
    expect(button).toHaveClass("bg-danger-600");
  });

  it("renders button with small size", () => {
    render(<Button size="sm">Small</Button>);
    const button = screen.getByRole("button", { name: /small/i });
    expect(button).toHaveClass("px-3", "py-1", "text-sm");
  });

  it("renders button with large size", () => {
    render(<Button size="lg">Large</Button>);
    const button = screen.getByRole("button", { name: /large/i });
    expect(button).toHaveClass("px-6", "py-3", "text-lg");
  });

  it("renders disabled button", () => {
    render(<Button disabled>Disabled</Button>);
    const button = screen.getByRole("button", { name: /disabled/i });
    expect(button).toBeDisabled();
  });

  it("renders button with fullWidth", () => {
    render(<Button fullWidth>Full Width</Button>);
    const button = screen.getByRole("button", { name: /full width/i });
    expect(button).toHaveClass("w-full");
  });

  it("calls onClick handler when clicked", () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    const button = screen.getByRole("button", { name: /click/i });
    button.click();
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("renders loading state", () => {
    render(<Button loading>Loading</Button>);
    const button = screen.getByRole("button", { name: /loading/i });
    expect(button).toBeDisabled();
  });
});
