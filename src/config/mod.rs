//! Configuration Module
//!
//! Handles provider configuration loading and validation.

pub mod loader;
pub mod provider;

pub use loader::ConfigLoader;
pub use provider::{
    KeyPoolConfig, ModelConfig, ProviderConfig, ProviderRegistry, ProvidersConfig, RateLimitConfig,
    RotationStrategy, SpecialHandling,
};
