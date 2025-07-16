import mongoose from "mongoose";

const subscriptionSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "Subscription Name is Required"],
      trim: true,
      minLength: 3,
      maxLength: 100,
    },
    price: {
      type: Number,
      required: [true, "Subscription Price is Required"],
      min: [0, "Price must be greater than 0"],
    },
    currency: {
      type: String,
      required: [true, "Currency is Required"],
      enum: ["USD", "EUR", "GBP", "INR", "IDR"], // Add more currencies as needed
    },
    frequency: {
      type: String,
      required: [true, "Subscription Frequency is Required"],
      enum: ["daily", "weekly", "monthly", "yearly"], // Add more frequencies as needed
    },
    category: {
      type: String,
      required: [true, "Subscription Category is Required"],
      enum: [
        "sports",
        "entertainment",
        "health",
        "politics",
        "technology",
        "lifestyle",
        "other",
      ], // Add more categories as needed
    },
    paymentMethod: {
      type: String,
      required: [true, "Payment Method is Required"],
      trim: true,
    },
    status: {
      type: String,
      required: [true, "Subscription Status is Required"],
      enum: ["active", "inactive", "cancelled", "expired"], // Add more statuses as needed
      default: "active",
    },
    startDate: {
      type: Date,
      required: [true, "Subscription Start Date is Required"],
      validate: {
        validator: (value) => value <= new Date(),
        message: "Start Date must be in the past",
      },
    },
    renewalDate: {
      type: Date,
      validate: {
        validator: function (value) {
          return value > this.startDate;
        },
        message: "Renewal date must be after the start date",
      },
    },
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: [true, "User ID is Required"],
      index: true, // Indexing user field for faster queries
      validate: {
        validator: function (value) {
          return mongoose.Types.ObjectId.isValid(value);
        },
        message: "Invalid User ID format",
      },
    },
  },
  { timestamps: true }
);
subscriptionSchema.pre("save", function (next) {
  if (!this.renewalDate) {
    const renewalPeriods = {
      daily: 1,
      weekly: 7,
      monthly: 30,
      yearly: 365,
    };

    this.renewalDate = new Date(this.startDate);
    this.renewalDate.setDate(
      this.startDate.getDate() + renewalPeriods[this.frequency]
    );
  }

  if (this.renewalDate < new Date()) {
    this.status = "expired";
  }

  next();
});

const Subscription = mongoose.model("Subscription", subscriptionSchema);
export default Subscription;
