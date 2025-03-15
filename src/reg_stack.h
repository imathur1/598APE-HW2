#pragma once

#include <algorithm>

namespace genetic {

/**
 * @brief A fixed capacity stack on device currently used for AST evaluation
 *
 * The idea is to use only the registers to store the elements of the stack,
 * thereby achieving the best performance.
 *
 * @tparam DataT   data type of the stack elements
 * @tparam MaxSize max capacity of the stack
 */
template <typename DataT, int MaxSize> struct stack {
  explicit stack() : elements_(0) {
    std::fill(regs_, regs_ + MaxSize, DataT(0));
  }

  /** Checks if the stack is empty */
  inline bool empty() const { return elements_ == 0; }

  /** Current number of elements in the stack */
  inline int size() const { return elements_; }

  /** Checks if the number of elements in the stack equal its capacity */
  inline bool full() const { return elements_ == MaxSize; }

  /**
   * @brief Pushes the input element to the top of the stack
   *
   * @param[in] val input element to be pushed
   *
   * @note If called when the stack is already full, then it is a no-op! To keep
   *       the device-side logic simpler, it has been designed this way. Trying
   *       to push more than `MaxSize` elements leads to all sorts of incorrect
   *       behavior.
   */
  inline void push(DataT val) { regs_[elements_++] = val; }

  /**
   * @brief Lazily pops the top element from the stack
   *
   * @return pops the element and returns it, if already reached bottom, then it
   *         returns zero.
   *
   * @note If called when the stack is already empty, then it just returns a
   *       value of zero! To keep the device-side logic simpler, it has been
   *       designed this way. Trying to pop beyond the bottom of the stack leads
   *       to all sorts of incorrect behavior.
   */
  inline DataT pop() { return regs_[--elements_]; }

private:
  int elements_;
  DataT regs_[MaxSize];
}; // struct stack

} // namespace genetic
